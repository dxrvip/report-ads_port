import { useRecordContext } from "react-admin";
import { Link, Tooltip, Typography} from "@mui/material";

function MyTextField({ source, label }: { source: string, label: string }) {
  const record = useRecordContext();

  if (!record) return null;
  return (
    <>
      <Typography
        variant='inherit'
      >
        <Tooltip title={record[source]} arrow>
            <span style={{display: "inline-block",width: "200px", height: "20px", overflow: "hidden", whiteSpace: "nowrap",textOverflow: "ellipsis"}}>{record[source]}</span>
        </Tooltip>
      </Typography>
    </>
  );
}

export default MyTextField;
