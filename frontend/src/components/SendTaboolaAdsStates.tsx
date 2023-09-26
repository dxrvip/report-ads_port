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

  const send = async (active: boolean) => {
    // const url = `https://tab.jordonfbi.uk/api/v1/list/taboola/update_campaign/${record.id}?active=${active}`;
    const url = `http://localhost:8000/api/v1/list/taboola/update_campaign/${record.id}?active=${active}`;
    const options = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    };
    const response = await fetch(url, options as any)
    if (response.status == 201){
        const res = await response.json()
        notify(res.msg, { type: "success" });
    }else{
      notify("修改失败！", { type: "error" });
    }
      refresh();
      handleClose();

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
        color={record.promotion ?  'error' : 'success' }
        onClick={(e) => {
          e.stopPropagation();
          handleOpen();
          send(record.promotion);
          return false;
        }}
      >
        {record.promotion ?  "禁用": "开启"}
      </Button>
    </>
  );
}

export default SendTaboolaAdsStates;
