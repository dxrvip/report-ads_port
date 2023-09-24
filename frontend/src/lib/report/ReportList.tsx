import {
  List,
  Datagrid,
  TextField,
  useGetRecordId,
  DateField,
  Identifier,
  RaRecord,
  BooleanField,
} from "react-admin";
import { useState } from "react";
import { SwipeableDrawer } from "@mui/material";
import ReportShow from "./ReportShow";
import MyUrlField from "../../components/MyUrlFile";

const ReportList = (props: any) => {
  const recordId = useGetRecordId();
  const [currId, setCurrId] = useState<Identifier>();
  const [show, setShow] = useState(false);
  const postRowClick = (id: Identifier, resource: string, record: RaRecord) => {
    setShow(true);
    setCurrId(id);
    return false;
  };
  const toggleDrawer =
    (open: boolean) => (event: React.KeyboardEvent | React.MouseEvent) => {
      if (
        event &&
        event.type === "keydown" &&
        ((event as React.KeyboardEvent).key === "Tab" ||
          (event as React.KeyboardEvent).key === "Shift")
      ) {
        return;
      }

      setShow(open);
    };
  return (
    <div>
      <List
        storeKey={false}
        disableSyncWithLocation
        resource="list/report"
        actions={false}
        filter={{ domain_id: recordId }}
        title="/访客"
      >
        <Datagrid rowClick={postRowClick as any}>
          <TextField source="id" />
          <DateField source="create" showTime label="浏览时间" />
          <MyUrlField source="url" />
          <TextField source="browser_info.fingerprint_id" label="指纹ID" />
          <TextField source="visitor.ip" label="Ip" />
          <TextField source="taboola_id" label="TaboolaId" />
          <TextField
            source="browser_info.equipment.browser[0]"
            label="浏览器"
          />
          <TextField source="browser_info.equipment.os[0]" label="设备" />
          <BooleanField source="browser_info.equipment.is_bot" label="机器人" />
        </Datagrid>
      </List>
      <SwipeableDrawer
        anchor="right"
        open={!!show}
        onClose={toggleDrawer(false)}
        onOpen={toggleDrawer(false)}
        sx={{ zIndex: 100 }}
      >
        <ReportShow id={currId} />
      </SwipeableDrawer>
    </div>
  );
};

export default ReportList;
