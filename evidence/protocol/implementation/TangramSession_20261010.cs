using System;
using System.IO;
using Unity.Netcode;
using Unity.Netcode.Transports.UTP;
using UnityEngine;
using UnityEngine.UI;

namespace REIT.Tangram
{
    public enum StudyView { FirstPerson, Overhead }
    public enum SessionAction { Previous, Next, Answer, Reset, View, Start, Pause, Finish, Practice }

    // One server-owned state is used by both peers; the local XR rig is never network-spawned.
    public class TangramSession : NetworkBehaviour
    {
        public static TangramSession Instance { get; private set; }
        public NetworkManager manager;
        public UnityTransport transport;
        public TangramView localView;
        public TangramPiece[] pieces;
        public Image taskImage;
        public Sprite[] silhouettes, solutions;
        public string[] taskIds;
        public string hostAddress = "192.168.1.100";
        public ushort port = 7777;
        [Tooltip("0 disables the round limit; the facilitator finishes the round manually.")]
        public float roundLimitSeconds = 0;
        public string pairCode = "TECHNICAL_TEST";
        [NonSerialized] public string RoomPin="",JoinPin="";
        public NetworkVariable<int> Task = new NetworkVariable<int>(0);
        public NetworkVariable<int> View = new NetworkVariable<int>(0);
        public NetworkVariable<int> Epoch = new NetworkVariable<int>(0);
        public NetworkVariable<bool> Answer = new NetworkVariable<bool>(false);
        public NetworkVariable<bool> Practice = new NetworkVariable<bool>(true);
        public NetworkVariable<bool> Running = new NetworkVariable<bool>(false);
        public NetworkVariable<bool> Paused = new NetworkVariable<bool>(false);
        public NetworkVariable<double> StartedAt = new NetworkVariable<double>(0);
        public NetworkVariable<double> PauseAt = new NetworkVariable<double>(0);
        public NetworkVariable<double> PauseTotal = new NetworkVariable<double>(0);
        public NetworkVariable<double> FinishedElapsed = new NetworkVariable<double>(0);
        public string Status { get; private set; } = "Offline — create or join a room";
        StreamWriter log;
        TangramResearchLog researchLog;
        int nextResearchRound=1, researchRound;
        double researchStarted, researchEnded=-1, researchActiveEnded;
        public string ResearchLogPath => researchLog?.FilePath ?? "";
        public string ResearchLogError {get;private set;} = "";
        public int NextResearchRound => nextResearchRound;
        public string ResearchRoundId => researchRound>0 ? pairCode+"-R"+researchRound.ToString("D2") : "";
        const string ResearchProtocol="REIT7841-20261008-shared-target-unlimited-menu-v1";
        public bool ResearchRecording => IsServer && Running.Value && !Paused.Value && researchLog!=null;
        bool joining;float joinDeadline;
        int renderedTask=-1; bool renderedAnswer; float lastLogFlush;
        public bool Ready => IsSpawned && manager.IsListening;
        public bool CanManipulate => Ready && !Paused.Value && (Practice.Value || Running.Value);
        public double Elapsed => !Ready ? 0 : !Running.Value ? FinishedElapsed.Value : Math.Max(0,(Paused.Value ? PauseAt.Value : manager.ServerTime.Time)-StartedAt.Value-PauseTotal.Value);

        void Awake()
        {
            Instance=this;
            manager.ConnectionApprovalCallback=Approve;
            manager.OnClientConnectedCallback+=Connected;
            manager.OnClientDisconnectCallback+=Disconnected;
            manager.OnTransportFailure+=TransportFailure;
        }
        void Approve(NetworkManager.ConnectionApprovalRequest request, NetworkManager.ConnectionApprovalResponse response)
        {
            string payload=System.Text.Encoding.ASCII.GetString(request.Payload ?? new byte[0]);
            bool version=payload.StartsWith(TangramLanRoom.Protocol+"|");
            bool code=string.IsNullOrEmpty(RoomPin) || payload==TangramLanRoom.Protocol+"|"+RoomPin;
            response.Approved=manager.ConnectedClientsIds.Count<2 && version && code;
            response.CreatePlayerObject=response.Approved;
            response.Reason=response.Approved?"":!version?"Both headsets need the same no-time-limit version.":!code?"Room code does not match.":"This room already has two players.";
            response.Pending=false;
        }
        public void Host()
        {
            if(manager.IsListening)return;
            transport.SetConnectionData("127.0.0.1",port,"0.0.0.0");
            manager.NetworkConfig.ConnectionData=System.Text.Encoding.ASCII.GetBytes(TangramLanRoom.Protocol+"|"+RoomPin);
            Status=manager.StartHost()?"Room open — waiting for second player":"Could not start host";
        }
        public void Join()
        {
            if(manager.IsListening)return;
            if(!System.Net.IPAddress.TryParse(hostAddress,out var ip) || ip.AddressFamily!=System.Net.Sockets.AddressFamily.InterNetwork)
            { Status="Enter the host's IPv4 address"; return; }
            transport.SetConnectionData(hostAddress,port);
            manager.NetworkConfig.ConnectionData=System.Text.Encoding.ASCII.GetBytes(TangramLanRoom.Protocol+"|"+JoinPin);
            joining=manager.StartClient();joinDeadline=Time.unscaledTime+15;
            Status=joining?"Connecting to "+hostAddress:"Could not start client";
        }
        public void Leave(){joining=false;if(manager.IsListening)manager.Shutdown(); Status="Disconnected"; }
        void TransportFailure(){Status="Network transport failed — check Wi-Fi and address";}
        void Connected(ulong id)
        {
            if(id==manager.LocalClientId)joining=false;
            if(id==manager.LocalClientId) localView.ScheduleSeat(manager.IsHost ? 0 : 1);
            Status="Connected — "+(manager.IsHost ? "host" : "participant");
            Log("connected",id.ToString());
        }
        void Disconnected(ulong id)
        {
            if(IsServer)
            {
                foreach(var p in pieces)if(p!=null)p.ReleaseDisconnected(id);
                if(Running.Value && !Paused.Value){PauseAt.Value=manager.ServerTime.Time;Paused.Value=true;FreezePieces("disconnect");}
                Log("disconnected",id.ToString());
            }
            Status=!string.IsNullOrEmpty(manager.DisconnectReason)?manager.DisconnectReason:"A player disconnected; check the room before continuing";
        }
        public override void OnNetworkSpawn()
        {
            renderedTask=-1;
            if(IsServer)
            {
                string folder=Path.Combine(Application.persistentDataPath,"REIT_Tangram");
                Directory.CreateDirectory(folder);
                string safe=System.Text.RegularExpressions.Regex.Replace(pairCode,"[^a-zA-Z0-9_-]","_");
                log=new StreamWriter(Path.Combine(folder,safe+"_"+DateTime.UtcNow.ToString("yyyyMMdd_HHmmss")+".csv"));
                log.WriteLine("utc,server_seconds,pair,epoch,task,view,practice,event,detail");
                OpenResearchLog();
                Log("session_start","Manual completion; task audio recorded separately");
            }
        }
        public override void OnNetworkDespawn(){RecordResearch("session_end",reason:"network_despawn",flush:true);researchLog?.Dispose();researchLog=null;log?.Dispose();log=null;renderedTask=-1;localView.SetView(StudyView.FirstPerson);}
        public void Request(SessionAction action)
        {
            if(!Ready){Status="Create or join a room first";return;}
            ActServerRpc((int)action);
        }
        public void RequestView(StudyView view)
        {
            if(!Ready){localView.SetView(view);return;}
            if(Running.Value){Status="Finish the recorded round before changing its view condition";return;}
            SetViewServerRpc((int)view);
        }
        [ServerRpc(RequireOwnership=false)]
        void SetViewServerRpc(int view,ServerRpcParams rpc=default)
        {if(!Running.Value && (view==0 || view==1)){View.Value=view;Log("view_key",view.ToString());RecordResearch("view_selected",rpc.Receive.SenderClientId,reason:((StudyView)view).ToString());}}
        [ServerRpc(RequireOwnership=false)]
        void ActServerRpc(int code,ServerRpcParams rpc=default)
        {
            if(code<0 || code>(int)SessionAction.Practice)return;
            var action=(SessionAction)code;
            // Practice controls are equal; only recorded-round start/finish belong to the facilitator.
            if(rpc.Receive.SenderClientId!=NetworkManager.ServerClientId && (action==SessionAction.Start || action==SessionAction.Finish))return;
            if(Running.Value && action==SessionAction.Reset && rpc.Receive.SenderClientId!=NetworkManager.ServerClientId)return;
            switch(action)
            {
                case SessionAction.Previous: if(!Running.Value)SetTask(-1);break;
                case SessionAction.Next: if(!Running.Value)SetTask(1);break;
                case SessionAction.Answer: if(Practice.Value && !Running.Value)Answer.Value=!Answer.Value;break;
                case SessionAction.Reset: ResetTask("manual_reset");break;
                case SessionAction.View:
                    if(!Running.Value)View.Value=1-View.Value;break;
                case SessionAction.Practice:
                    if(!Running.Value){ResetTask("practice_change");Practice.Value=!Practice.Value;Answer.Value=false;}break;
                case SessionAction.Start:
                    if(manager.ConnectedClientsIds.Count!=2 || Running.Value)break;
                    ResetTask("round_prepare");Practice.Value=false;Answer.Value=false;
                    StartedAt.Value=manager.ServerTime.Time;Running.Value=true;Log("round_start","");break;
                case SessionAction.Pause:
                    if(!Running.Value && !Practice.Value)break;
                    if(!Paused.Value){PauseAt.Value=manager.ServerTime.Time;Paused.Value=true;FreezePieces("pause");}
                    else if(!Running.Value || manager.ConnectedClientsIds.Count==2)
                    {if(Running.Value)PauseTotal.Value+=manager.ServerTime.Time-PauseAt.Value;Paused.Value=false;}
                    Log("pause_state",Paused.Value.ToString());break;
                case SessionAction.Finish:
                    if(Running.Value){FinishedElapsed.Value=Elapsed;Log("completed_manual",Elapsed.ToString("F3",System.Globalization.CultureInfo.InvariantCulture));Running.Value=false;Paused.Value=false;FreezePieces("round_end_manual");}
                    break;
            }
            Log("action",action+" by "+rpc.Receive.SenderClientId);
            RecordResearch("control_action",rpc.Receive.SenderClientId,reason:action.ToString());
        }
        void SetTask(int delta){ResetTask("task_change");Task.Value=(Task.Value+delta+silhouettes.Length)%silhouettes.Length;Answer.Value=false;}
        void FreezePieces(string reason){Epoch.Value++;foreach(var p in pieces)p.ServerFreeze(Epoch.Value,reason);}
        void ResetTask(string reason)
        {
            if(Running.Value)Log("round_aborted",reason);
            Running.Value=false;Paused.Value=false;PauseTotal.Value=0;FinishedElapsed.Value=0;StartedAt.Value=manager.ServerTime.Time;
            Epoch.Value++;Answer.Value=false;
            foreach(var p in pieces)p.ServerReset(Epoch.Value);
            Log("reset",reason);
        }
        void Update()
        {
            if(joining && Time.unscaledTime>=joinDeadline){Leave();Status="Connection timed out. Check host IP / Wi-Fi, then edit address and retry.";}
            if(!Ready)return;
            if(IsServer && Running.Value && !Paused.Value && roundLimitSeconds>0 && Elapsed>=roundLimitSeconds)
            {FinishedElapsed.Value=Elapsed;Log("time_limit",Elapsed.ToString("F3"));Running.Value=false;FreezePieces("time_limit");}
            localView.SetView((StudyView)View.Value);
            if(renderedTask!=Task.Value || renderedAnswer!=Answer.Value)
            {
                renderedTask=Task.Value;renderedAnswer=Answer.Value;
                if(taskImage && renderedTask>=0 && renderedTask<silhouettes.Length)
                    taskImage.sprite=renderedAnswer ? solutions[renderedTask] : silhouettes[renderedTask];
            }
            if(Time.unscaledTime-lastLogFlush>1){log?.Flush();researchLog?.Flush();if(researchLog?.LastError!=null)ResearchLogError=researchLog.LastError;lastLogFlush=Time.unscaledTime;}
        }
        public void Log(string kind,string detail)
        {
            if(IsServer)
            {
                if(kind=="round_start")
                {
                    researchRound=nextResearchRound++;researchStarted=StartedAt.Value;researchEnded=-1;
                    RecordResearch("round_start",reason:"facilitator_start",extra:ViewContext(),flush:true);
                    foreach(var piece in pieces)if(piece)RecordPiece("piece_initial",null,piece,piece.Position.Value,piece.Rotation.Value);
                }
                else if(kind=="completed_manual" || kind=="time_limit" || kind=="round_aborted")
                {
                    researchEnded=manager.ServerTime.Time;researchActiveEnded=Elapsed;
                    RecordResearch(kind=="completed_manual"?"round_end_manual":kind,reason:detail,flush:true);
                    foreach(var piece in pieces)if(piece)RecordPiece("piece_at_round_end",null,piece,piece.transform.position,piece.transform.rotation);
                }
                else if(kind!="grab" && kind!="release" && kind!="disconnect_release" && kind!="action")
                    RecordResearch(kind,reason:detail,flush:kind=="pause_state" || kind=="disconnected");
            }
            if(log==null)return;
            string task=Task.Value<taskIds.Length?taskIds[Task.Value]:Task.Value.ToString();
            log.WriteLine(string.Join(",",DateTime.UtcNow.ToString("o"),manager.ServerTime.Time.ToString("F3",System.Globalization.CultureInfo.InvariantCulture),Quote(pairCode),Epoch.Value,Quote(task),View.Value,Practice.Value,Quote(kind),Quote(detail)));
        }

        void OpenResearchLog()
        {
            researchLog?.Dispose();researchLog=null;ResearchLogError="";
            try {researchLog=new TangramResearchLog(Path.Combine(Application.persistentDataPath,"REIT_Tangram","ResearchV2"),pairCode);}
            catch(Exception e){ResearchLogError=e.GetType().Name+": "+e.Message;Debug.LogWarning("REIT research logging unavailable: "+ResearchLogError);}
        }
        public bool ConfigureResearch(string group,int nextRound)
        {
            if(!IsServer || Running.Value || !System.Text.RegularExpressions.Regex.IsMatch(group??"","^G[0-9]{2}$") || group=="G00" || nextRound<1 || nextRound>99)return false;
            bool changed=pairCode!=group;
            if(changed)RecordResearch("session_group_change",reason:group,flush:true);
            pairCode=group;nextResearchRound=nextRound;researchRound=0;researchEnded=-1;
            if(changed || researchLog==null)OpenResearchLog();
            RecordResearch("study_setup",reason:"next_round_R"+nextRound.ToString("D2"),extra:ViewContext(),flush:true);
            Notify("Study "+group+" / next R"+nextRound.ToString("D2")+(ResearchLogError.Length>0?" / LOG ERROR":" / logging ready"));return ResearchLogError.Length==0;
        }
        public static string Participant(ulong client)=>client==NetworkManager.ServerClientId?"P1":"P2";
        public string PieceId(TangramPiece piece)
        {int i=Array.IndexOf(pieces,piece);return i>=0?"S"+(i+1):"UNREGISTERED";}
        string ViewContext()
        {
            if(!localView)return "";
            var camera=localView.overhead;
            return "host=P1;guest=P2;guest_overhead_optical_rotation_deg=0;target_presentation=shared-world-target-v1;target_board_count=1;target_orientation=fixed_world;target_depth_test=always;build_version=0.3.2-overhead-menu;menu_presentation=local_foreground;pose_space=Unity_world;length_unit=m;pose_sample_hz=10;avatar_sample_hz=2;motion_threshold_m=0.002;rotation_threshold_deg=2;round_limit_s="+TangramResearchLog.Number(roundLimitSeconds)+";round_end_policy="+(roundLimitSeconds>0?"manual_or_time_limit":"manual")+";overhead_camera="+(camera?camera.transform.position.ToString("F4")+" / "+camera.transform.rotation.ToString("F4"):"missing")+";fixed_material="+(localView.fixedOverheadMaterial?"yes":"no");
        }
        public void RecordResearch(string kind,ulong? actor=null,TangramPiece piece=null,Vector3? position=null,Quaternion? rotation=null,string manipulation="",string reason="",string extra="",bool flush=false,double? displacement=null,double? angle=null,bool? snapped=null)
        {
            if(!IsServer || researchLog==null)return;
            bool formal=researchRound>0 && !Practice.Value;
            double now=manager.ServerTime.Time;
            var data=new System.Collections.Generic.Dictionary<string,string>{
                {"protocol_version",ResearchProtocol},{"server_seconds",TangramResearchLog.Number(now)},
                {"pair_id",pairCode},{"round_id",formal?ResearchRoundId:""},{"round_index",formal?researchRound.ToString():""},
                {"task_id",Task.Value>=0&&Task.Value<taskIds.Length?taskIds[Task.Value]:Task.Value.ToString()},
                {"condition",View.Value==0?"VR_FIRST_PERSON":"VR_EXTERNAL"},
                {"phase",Practice.Value?"practice":researchEnded>=0?"ended":Running.Value?(Paused.Value?"paused":"task"):formal?"ended":"ready"},
                {"wall_elapsed_s",formal?TangramResearchLog.Number(Math.Max(0,(researchEnded>=0?researchEnded:now)-researchStarted)):""},
                {"active_elapsed_s",formal?TangramResearchLog.Number(researchEnded>=0?researchActiveEnded:Elapsed):""},{"epoch",Epoch.Value.ToString()},
                {"participant_id",actor.HasValue?Participant(actor.Value):""},{"client_id",actor.HasValue?actor.Value.ToString():""},
                {"piece_id",piece?PieceId(piece):""},{"piece_name",piece?piece.name:""},
                {"held_by",piece&&piece.Holder.Value!=ulong.MaxValue?Participant(piece.Holder.Value):""},
                {"manipulation_id",manipulation},{"reason",reason},{"extra",extra},
                {"displacement_m",displacement.HasValue?TangramResearchLog.Number(displacement.Value):""},
                {"rotation_change_deg",angle.HasValue?TangramResearchLog.Number(angle.Value):""},
                {"snapped",snapped.HasValue?(snapped.Value?"true":"false"):""}
            };
            if(position.HasValue){var p=position.Value;data["position_x_m"]=TangramResearchLog.Number(p.x);data["position_y_m"]=TangramResearchLog.Number(p.y);data["position_z_m"]=TangramResearchLog.Number(p.z);}
            if(rotation.HasValue){var q=rotation.Value;data["rotation_x"]=TangramResearchLog.Number(q.x);data["rotation_y"]=TangramResearchLog.Number(q.y);data["rotation_z"]=TangramResearchLog.Number(q.z);data["rotation_w"]=TangramResearchLog.Number(q.w);}
            if(!researchLog.Write(kind,data,flush))ResearchLogError=researchLog.LastError??"Logger write failed";
        }
        public void RecordPiece(string kind,ulong? actor,TangramPiece piece,Vector3 position,Quaternion rotation,string manipulation="",string reason="",bool? snapped=null,double? displacement=null,double? angle=null)
        {RecordResearch(kind,actor,piece,position,rotation,manipulation,reason,flush:kind=="grab_accepted"||kind=="piece_release",displacement:displacement,angle:angle,snapped:snapped);}
        [Serializable] class HandsContext {public Vector3 left,right;public Quaternion leftRotation,rightRotation;}
        public void RecordParticipantPose(ulong client,AvatarPose pose)
        {
            if(!ResearchRecording)return;
            RecordResearch("participant_pose",client,position:pose.head,rotation:pose.headRot,
                reason:"head_and_controller_pose_not_eye_gaze",extra:JsonUtility.ToJson(new HandsContext{left=pose.left,right=pose.right,leftRotation=pose.leftRot,rightRotation=pose.rightRot}));
        }
        void OnApplicationFocus(bool focus){if(IsServer)RecordResearch("application_focus",reason:focus?"gained":"lost",flush:true);}
        void OnApplicationPause(bool pause){if(IsServer)RecordResearch("application_pause",reason:pause?"paused":"resumed",flush:true);}
        void OnApplicationQuit(){researchLog?.Flush();log?.Flush();}

        static string Quote(string s)=>"\""+(s??"").Replace("\"","\"\"")+"\"";
        public void Notify(string message){Status=message;}
        public override void OnDestroy()
        {
            researchLog?.Dispose();
            log?.Dispose();
            if(manager){manager.OnClientConnectedCallback-=Connected;manager.OnClientDisconnectCallback-=Disconnected;manager.OnTransportFailure-=TransportFailure;}
            if(Instance==this)Instance=null;
            base.OnDestroy();
        }
    }
}
