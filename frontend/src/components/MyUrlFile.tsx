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
            <Link href={record[source]} style={{display: "inline-block",width: "200px", height: "20px", overflow: "hidden", whiteSpace: "nowrap",textOverflow: "ellipsis"}}>{record[source]}</Link>
        </Tooltip>
      </Typography>
    </>
  );
}

export default MyUrlField;
