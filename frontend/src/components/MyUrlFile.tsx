import { useRecordContext } from "react-admin";
import { Link, Tooltip, Typography} from "@mui/material";

function MyUrlField({ source }: { source: string }) {
  const record = useRecordContext();
  if (!record) return null;
  return (
    <>
      <Typography
        variant='inherit'
      >
        <Tooltip title={record[source]} arrow>
            <div style={{width: "200px", height: "20px", overflow: "hidden", whiteSpace: "nowrap",textOverflow: "ellipsis"}}>{record[source]}</div>
        </Tooltip>
      </Typography>
    </>
  );
}

export default MyUrlField;
