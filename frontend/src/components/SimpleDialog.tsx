import { Grid, Dialog, DialogTitle } from "@mui/material";
import SendTaboolaAdsStates from "./SendTaboolaAdsStates";
import {
  Datagrid,
  DateField,
  List,
  TextField,
  useRecordContext,
} from "react-admin";
import { Invoice } from "../types";
export interface SimpleDialogProps {
  open: boolean;
  onClose: (value: string) => void;
}

function SimpleDialog(props: SimpleDialogProps) {
  const { onClose, open } = props;
  const record = useRecordContext<Invoice>();

  if (!record) return null;

//   const handleListItemClick = (value: string) => {
//     onClose(value);
//   };
  return (
    <Dialog onClose={onClose} aria-labelledby="simple-dialog-title" fullWidth maxWidth={"md"} open={open}>
      <DialogTitle id="simple-dialog-title">siteId的数据明细</DialogTitle>
      <Grid item ml={6}>
        <List
          resource="list/taboola"
          actions={false}
          filter={{ record_id: record.id }}
          title={"."}
          debounce={1000}
          disableSyncWithLocation
        >
          <Datagrid>
            <TextField source="id" />
            <TextField source="site_id" label="siteId" />
            <DateField source="create" label="时间" showTime />
            <TextField source="page_sum" label="纵深" />
            <TextField source="post_sum" label="总文章数" />
            <TextField source="ip_sum" label="总访客数" />
            <TextField source="report_sum" label="累计浏览量" />
            <SendTaboolaAdsStates label="操作" />
          </Datagrid>
        </List>
      </Grid>
    </Dialog>
  );
}

export default SimpleDialog;
