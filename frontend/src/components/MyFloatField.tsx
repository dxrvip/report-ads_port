import { useRecordContext } from "react-admin";
import { Tooltip, Typography} from "@mui/material";

function MyFloatField({ source, label, reference }: { source: string, label: string , reference: GLfloat}) {
  const record = useRecordContext();

  if (!record) return null;
  return (
    <>
      <Typography
        variant='inherit'
        color={record[source] > reference ? "red" : ''}
      >
          {record[source]?.toFixed(2)}
      </Typography>
    </>
  );
}

export default MyFloatField;
