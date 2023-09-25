import { useRecordContext, useNotify, useRefresh } from "react-admin";
import { CircularProgress, Backdrop, Button } from "@mui/material";
import { useState } from "react";
interface Send {
  (active?: boolean): string;
}

function SendTaboolaAdsStates({ label }: { label: string }) {
  const record = useRecordContext();
  const notify = useNotify();
  const refresh = useRefresh();
  const [open, setOpen] = useState(false);
  const handleClose = () => {
    setOpen(false);
  };
  const handleOpen = () => {
    setOpen(true);
  };
  if (!record) return null;

  const send: Send = (active) => {
    const url = `https://tab.jordonfbi.uk/api/v1/list/taboola/update_campaign/${record.id}?active=${active}`;
    // const url = `http://localhost:8000/api/v1/list/taboola/update_campaign/${record.id}?active=${active}`;
    const options = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    };
    fetch(url, options as any)
      .then((response) => {
        notify("修改成功！", { type: "success" });
        refresh();
        handleClose();
      })
      .catch((error) => {
        notify("修改失败！", { type: "error" });
        handleClose();
      })
      .finally(() => {
        // notify("修改超时！", { type: "error" });
        handleClose();
      });
    return "";
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
        color={record.promotion == 1 ? 'warning' : 'success'}
        onClick={(e) => {
          e.stopPropagation();
          handleOpen();
          const active = record.promotion == 1 ? false : true;
          send(active);
          return false;
        }}
      >
        {record.promotion == 1 ? "停止推广" : "开启推广"}
      </Button>
    </>
  );
}

export default SendTaboolaAdsStates;
