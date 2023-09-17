import { useRecordContext } from "react-admin";
import { Link, Tooltip, Button } from "@mui/material";
import { useState } from "react";
interface Send {
  (active?: boolean): string;
}
interface Response {
  msg?: string;
}
function SendTaboolaAdsStates({ label }: { label: string }) {
  const record = useRecordContext();
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
    });
    return "cg";
  };
  return (
    <>
      <Button
        disabled={!record?.promotion ? false : true}
        onClick={(e) => {
          e.stopPropagation();
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
