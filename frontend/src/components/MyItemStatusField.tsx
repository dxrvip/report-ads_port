import { useRecordContext } from "react-admin";
import PlayCircleFilledWhiteRoundedIcon from "@mui/icons-material/PlayCircleFilledWhiteRounded";
import StopCircleRoundedIcon from '@mui/icons-material/StopCircleRounded';

function MyItemStatusField({
  source,
  label,
}: {
  source: string;
  label: string;
}) {
  const record = useRecordContext();

  if (!record) return null;
  const x = record["item_count"] - record["item_status"];
  const start_arr = Array.from(
    Array(record["item_status"]).keys(),
    (n) => n + 1
  );
  // console.log(start_arr);

  const stop_arr =Array.from(
    Array(x).keys(),
    (n) => n + 1
  );
  return (
    <>
      {start_arr.map((i) => (
        <span key={i}>
          <PlayCircleFilledWhiteRoundedIcon fontSize="small" color="success" />
        </span>
      ))}
      {stop_arr.map((i) => (
        <span key={i}>
          <StopCircleRoundedIcon fontSize="small" color="action" />
        </span>
      ))}
    </>
  );
}

export default MyItemStatusField;
