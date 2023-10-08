import { useRecordContext } from "react-admin";
import PlayCircleFilledWhiteRoundedIcon from "@mui/icons-material/PlayCircleFilledWhiteRounded";
import StopCircleRoundedIcon from "@mui/icons-material/StopCircleRounded";
import ItemDialog from "./ItemDialog";
import { useState } from "react";

function MyItemStatusField({
  source,
  label,
}: {
  source: string;
  label: string;
}) {
  const record = useRecordContext();
  const [open, setOpen] = useState(false);
  if (!record) return null;

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    return false;
  };
  const x = record["item_count"] - record["item_status"];
  const start_arr = Array.from(
    Array(record["item_status"]).keys(),
    (n) => n + 1
  );
  // console.log(start_arr);

  const stop_arr = Array.from(Array(x).keys(), (n) => n + 1);
  
  if (record["item_status_count"] === 0) {
    const total_arr = Array.from(
      Array(record["item_count"]).keys(),
      (n) => n + 1
    );
    return (
      <div onClick={handleClickOpen}>
        {total_arr.map((i) => (
          <PlayCircleFilledWhiteRoundedIcon fontSize="small" color="success" />
        ))}
        <ItemDialog open={open} onClose={handleClose} />
      </div>
    );
  }
  return (
    <div
      onClick={(e) => {
        e.stopPropagation();        
        handleClickOpen();
        return;
      }}
    >
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
      <ItemDialog open={open} onClose={handleClose} />
    </div>
  );
}

export default MyItemStatusField;
