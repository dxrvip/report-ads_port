import { useRecordContext, useNotify, useRefresh } from "react-admin";
import { CircularProgress, Backdrop, Button } from "@mui/material";
import React from "react";
interface Send {
  (active?: boolean): string;
}

function SendPostAdsStates({ label }: { label: string }) {
  const record = useRecordContext();
  const notify = useNotify();
  const refresh = useRefresh();
  const [open, setOpen] = React.useState(false);
  const handleClose = () => {
    setOpen(false);
  };
  const handleOpen = () => {
    setOpen(true);
  };
  if (!record) return null;
  const send: Send = (active) => {
    const url = `https://tab.jordonfbi.uk/api/v1/list/post/update_campaign/${record.id}?active=${active}`;
    // const url = `http://localhost:8000/api/v1/list/post/update_campaign/${record.id}?active=${active}`;
    const options = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    };
    fetch(url, options as any)
      .then(async (response) => {
        if(response.status == 200){
          notify(`修改成功！`, { type: "success" });
        }else{
          const result = await response.json()
          notify(result.detail, { type: "error" });
          
        }
      
        refresh();
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
        color={record?.status===true || record.status === null ? 'warning' : 'success'}
        onClick={(e) => {
          e.stopPropagation();
          handleOpen();
          send(!record.status ? true : false);
          return false;
        }}
      >
        {record?.status===true || record.status === null ? "暂停" : "开启"}
      </Button>
    </>
  );
}

export default SendPostAdsStates;
