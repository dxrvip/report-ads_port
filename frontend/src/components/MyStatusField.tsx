import { useRecordContext } from "react-admin";
import { Chip, Typography } from "@mui/material";

function MyStatusField({ source, label }: { source: string; label: string }) {
  const record = useRecordContext();

  if (!record) return null;
  return (
    <>
      <Typography variant="inherit">
        <Chip
          label={record.promotion ? "开启" : "暂停"}
          color={record.promotion ? "success" : "error"}
          size="small"
          variant="outlined"
        />
      </Typography>
    </>
  );
}

export default MyStatusField;
