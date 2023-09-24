import { Grid, Dialog, DialogTitle, DialogContent } from "@mui/material";
import IconButton from "@mui/material/IconButton";
import SendTaboolaAdsStates from "./SendTaboolaAdsStates";
import CloseIcon from "@mui/icons-material/Close";
import { styled } from "@mui/material/styles";
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
  onClose: () => void;
}

export function CaceZsField({
  source,
  label,
}: {
  source: string;
  label: string;
}) {
  const record = useRecordContext<Invoice>();

  if (!record) return null;

  return <span>{record[source] > 0 ? record[source] : 0}</span>;
}
function SimpleDialog(props: SimpleDialogProps) {
  const { onClose, open } = props;
  const record = useRecordContext<Invoice>();

  if (!record) return null;

  //   const handleListItemClick = (value: string) => {
  //     onClose(value);
  //   };
  return (
    <Dialog
      onClose={(event: any) => {
        event.stopPropagation();
        onClose();
        return;
      }}
      aria-labelledby="simple-dialog-title"
      fullWidth
      maxWidth={"lg"}
      open={open}
    >
      <DialogTitle id="simple-dialog-title">siteId的数据明细</DialogTitle>
      <IconButton
        aria-label="close"
        sx={{
          position: "absolute",
          right: 8,
          top: 8,
          color: (theme) => theme.palette.grey[500],
        }}
        onClick={(e) => {
          e.stopPropagation();
          onClose();
          return;
        }}
      >
        <CloseIcon />
      </IconButton>
      <DialogContent onClick={(e) => e.stopPropagation()}>
        <Grid item ml={6}>
          <List
            disableSyncWithLocation
            resource="list/taboola"
            actions={false}
            storeKey={false}
            filter={{ post_id: record.id }}
            title={"."}
            debounce={1000}            
          >
            <Datagrid>
              <TextField source="id" />
              <TextField source="site_id" label="siteId" />
              <DateField source="create" label="时间" showTime />
              <TextField source="site" label="平台名称" />
              <TextField source="page_sum" label="翻页总数" />
              <TextField source="zs_sum" label="有纵深行为访客数" />
              <TextField source="ads_count" label="广告点击数" />
              <TextField source="ip_count" label="Ip访客总数" />
              <TextField source="tab_open_sum" label="siteId进入数" />
              <TextField source="borwser_count" label="指纹访客总数" />
              <TextField source="report_count" label="累计浏览量" />
              <SendTaboolaAdsStates label="操作" />
            </Datagrid>
          </List>
        </Grid>
      </DialogContent>
    </Dialog>
  );
}

export default SimpleDialog;
