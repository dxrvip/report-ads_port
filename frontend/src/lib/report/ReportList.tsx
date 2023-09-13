import {
  List,
  Datagrid,
  TextField,
  useGetRecordId,
  DateField,
  Identifier,
  RaRecord,
} from "react-admin";
import { useCallback, useState } from 'react';
import { matchPath, useLocation, useNavigate } from "react-router-dom";
import { slugStyle } from "./List";
import { Box, SwipeableDrawer, useMediaQuery, Theme } from "@mui/material";
import ReviewEdit from "./ReportShow";
import ReportShow from "./ReportShow";

const ReportList = (props: any) => {
  const recordId = useGetRecordId();
  const [currId, setCurrId] = useState<Identifier>()
  const [show, setShow] = useState(false)
  const postRowClick = (id: Identifier, resource: string, record: RaRecord) => {
    setShow(true)
    setCurrId(id)
    return false
  }
  const toggleDrawer = (open: boolean) => (
    event: React.KeyboardEvent | React.MouseEvent,
  ) => {
    if (
      event &&
      event.type === 'keydown' &&
      ((event as React.KeyboardEvent).key === 'Tab' ||
        (event as React.KeyboardEvent).key === 'Shift')
    ) {
      return;
    }

    setShow(open);
  };
  return (
    <div>
      <List
        resource="list/report"
        actions={false}
        filter={{ record_id: recordId }}
        title="/访客"
      >
        <Datagrid rowClick={postRowClick as any}>
          <TextField source="id" />
          <DateField source="create" showTime label="浏览时间" />
          <TextField source="url" sx={slugStyle} />
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
