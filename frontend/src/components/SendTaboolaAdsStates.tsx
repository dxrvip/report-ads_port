import { useRecordContext } from "react-admin";
import { CircularProgress, Backdrop, Button } from "@mui/material";
import { useState } from "react";
interface Send {
  (active?: boolean): string;
}
interface Response {
  msg?: string;
}
function SendTaboolaAdsStates({ label }: { label: string }) {
  const record = useRecordContext();
  const [open, setOpen] = useState(false);
  const handleClose = () => {
    setOpen(false);
  };
  const handleOpen = () => {
    setOpen(true);
  };
  if (!record) return null;
  const send: Send = (active) => {
    const url = `http://localhost:8000/api/v1/list/taboola/update_campaign/${record.id}?active=${active}`;
    const options = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };
    fetch(url, options).then((response) => {
      console.log(response?.msg);
      handleClose()
    });
    return "cg";
  };
  return (
    <>
      <Backdrop
        sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={open}
      >
        <CircularProgress color="inherit" />
      </Backdrop>
      <Button
        disabled={record?.promotion ? true : false}
        onClick={(e) => {
          e.stopPropagation();
          handleOpen()
          send(!record.promotion ? true : false);
          return false;
        }}
      >
        停止推广
      </Button>
    </>
  );
}

export default SendTaboolaAdsStates;
