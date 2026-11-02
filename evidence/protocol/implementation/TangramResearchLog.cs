using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Text;

namespace REIT.Tangram
{
    // CSV transport only. Psychological interpretations belong in subsequent video/audio coding.
    public sealed class TangramResearchLog : IDisposable
    {
        public const string SchemaVersion = "2.0";
        public static readonly string[] Columns = {
            "schema_version", "protocol_version", "session_id", "event_seq", "utc",
            "server_seconds", "pair_id", "round_id", "round_index", "task_id", "condition",
            "phase", "wall_elapsed_s", "active_elapsed_s", "epoch", "event",
            "participant_id", "client_id", "piece_id", "piece_name", "held_by",
            "manipulation_id", "reason", "position_x_m", "position_y_m", "position_z_m",
            "rotation_x", "rotation_y", "rotation_z", "rotation_w", "displacement_m",
            "rotation_change_deg", "snapped", "extra"
        };
        readonly StreamWriter writer;
        long sequence;
        bool disposed;
        public string FilePath { get; private set; }
        public string SessionId { get; private set; }
        public string LastError { get; private set; }
        public long EventCount => sequence;

        public TangramResearchLog(string folder, string pair)
        {
            Directory.CreateDirectory(folder);
            string safe = System.Text.RegularExpressions.Regex.Replace(pair ?? "UNSET", "[^a-zA-Z0-9_-]", "_");
            SessionId = DateTime.UtcNow.ToString("yyyyMMddTHHmmss", CultureInfo.InvariantCulture) + "_" + Guid.NewGuid().ToString("N").Substring(0, 8);
            FilePath = Path.Combine(folder, safe + "_" + SessionId + "_events_v2.csv");
            writer = new StreamWriter(FilePath, false, new UTF8Encoding(true));
            writer.WriteLine(string.Join(",", Columns));
            writer.Flush();
        }

        public bool Write(string kind, IDictionary<string, string> values, bool flush = false)
        {
            if (disposed || LastError != null) return false;
            try
            {
                var row = new string[Columns.Length];
                for (int i = 0; i < Columns.Length; i++)
                    row[i] = values != null && values.TryGetValue(Columns[i], out var value) ? value : "";
                row[0] = SchemaVersion;
                row[2] = SessionId;
                row[3] = (++sequence).ToString(CultureInfo.InvariantCulture);
                row[4] = DateTime.UtcNow.ToString("o", CultureInfo.InvariantCulture);
                row[15] = kind ?? "";
                for (int i = 0; i < row.Length; i++) row[i] = Quote(row[i]);
                writer.WriteLine(string.Join(",", row));
                if (flush) writer.Flush();
                return true;
            }
            catch (Exception e) { LastError = e.GetType().Name + ": " + e.Message; return false; }
        }
        public void Flush()
        {
            if (disposed || LastError != null) return;
            try { writer.Flush(); } catch (Exception e) { LastError = e.GetType().Name + ": " + e.Message; }
        }
        public void Dispose()
        {
            if (disposed) return;
            disposed = true;
            try { writer.Dispose(); } catch (Exception e) { LastError = e.GetType().Name + ": " + e.Message; }
        }
        public static string Number(double value) => double.IsNaN(value) || double.IsInfinity(value) ? "" : value.ToString("F6", CultureInfo.InvariantCulture);
        public static string Quote(string value) => "\"" + (value ?? "").Replace("\"", "\"\"") + "\"";
    }
}
