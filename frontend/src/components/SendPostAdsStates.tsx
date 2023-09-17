import { useRecordContext } from "react-admin";
import { CircularProgress, Backdrop, Button } from "@mui/material";
import React from "react";
interface Send {
  (active?: boolean): string;
}
interface Response {
  msg?: string;
}
function SendPostAdsStates({ label }: { label: string }) {
  const record = useRecordContext();
  const [open, setOpen] = React.useState(false);
  const handleClose = () => {
    setOpen(false);
  };
  const handleOpen = () => {
    setOpen(true);
  };
  if (!record) return null;
  const send: Send = (active) => {
    const url = `http://localhost:8000/api/v1/list/post/update_campaign/${record.id}?active=${active}`;
    const options = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };
    fetch(url, options).then((response) => {
      handleClose();
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
        onClick={(e) => {
          e.stopPropagation();
          handleOpen();
          send(!record.promotion ? true : false);
          return false;
        }}
      >
        {record?.promotion ? "暂停推广" : "开启推广"}
      </Button>
    </>
  );
}

export default SendPostAdsStates;
