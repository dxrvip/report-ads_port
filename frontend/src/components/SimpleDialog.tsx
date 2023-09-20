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
const BootstrapDialog = styled(Dialog)(({ theme }) => ({
  "& .MuiDialogContent-root": {
    padding: theme.spacing(2),
  },
  "& .MuiDialogActions-root": {
    padding: theme.spacing(1),
  },
}));
function SimpleDialog(props: SimpleDialogProps) {
  const { onClose, open } = props;
  const record = useRecordContext<Invoice>();

  if (!record) return null;

  //   const handleListItemClick = (value: string) => {
  //     onClose(value);
  //   };
  return (
    <Dialog
      onClose={(event: any)=>{
        event.stopPropagation()
        onClose()
        return
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
          e.stopPropagation()
          onClose();
          return
        }}
      >
        <CloseIcon />
      </IconButton>
      <DialogContent onClick={(e)=> e.stopPropagation()}>
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
              <TextField source="page_sum" label="翻页" />
              <TextField source="zonsen_sum" label="纵深" />
              <TextField source="post_sum" label="总文章数" />
              <TextField source="ip_sum" label="总访客数" />
              <TextField source="report_sum" label="累计浏览量" />
              <SendTaboolaAdsStates label="操作" />
            </Datagrid>
          </List>
        </Grid>
      </DialogContent>
    </Dialog>
  );
}

export default SimpleDialog;
