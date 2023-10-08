import { Grid, Dialog, DialogTitle, DialogContent } from "@mui/material";
import IconButton from "@mui/material/IconButton";
import SendPostAdsStates from "../components/SendPostAdsStates";
import CloseIcon from "@mui/icons-material/Close";
import {
  BooleanInput,
  DatagridConfigurable,
  DateInput,
  FilterButton,
  List,
  SelectColumnsButton,
  TextField,
  TextInput,
  TopToolbar,
  useRecordContext,
} from "react-admin";
import { Invoice } from "../types";
import MyFloatField from "./MyFloatField";
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
const ListActions = () => (
  <TopToolbar>
    <SelectColumnsButton />
    <FilterButton />
  </TopToolbar>
);
const postFilters = [
  <DateInput label="浏览日期" source="create_time" alwaysOn />,
];
function ItemDialog(props: SimpleDialogProps) {
  const { onClose, open } = props;
  const record = useRecordContext<Invoice>();

  if (!record) return null;

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
      <DialogTitle id="simple-dialog-title">文章的推广计划</DialogTitle>
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
            resource="items"
            actions={<ListActions />}
            exporter={false}
            storeKey={false}
            filter={{ post_id: record.id }}
            filters={postFilters}
            debounce={1000}
          >
            <DatagridConfigurable>
              <TextField source="id" sortable={false} label="ItemID" />
              <TextField source="campaign_id" sortable={false} label="campaignID" />
              <TextField source="page_sum" label="翻页总数" sortable={false} />
              <TextField
                source="zs_sum"
                label="有纵深行为访客数"
                sortable={false}
              />
              <TextField
                source="taboola_count"
                label="siteId总数"
                sortable={false}
              />
              <TextField source="page_sum" label="翻页总数" sortable={false} />
              <TextField
                source="zs_sum"
                label="有纵深行为访客数"
                sortable={false}
              />
              <MyFloatField
                source="page_zs"
                label="翻页/site进入数"
                reference={4}
              />
              <TextField
                source="ads_count"
                label="广告点击数"
                sortable={false}
              />
              <TextField
                source="ip_count"
                label="Ip访客总数"
                sortable={false}
              />
              <TextField
                source="tab_open_sum"
                label="siteId进入数"
                sortable={false}
              />
              <MyFloatField
                source="zs_site_open"
                label="纵深/site进入数"
                reference={0.3}
              />
              <TextField
                source="borwser_count"
                label="指纹访客总数"
                sortable={false}
              />
              <TextField
                source="report_count"
                label="累计浏览量"
                sortable={false}
              />
              <TextField
                source="ads_show_sum"
                label="广告显示计数"
                sortable={false}
              />
              <SendPostAdsStates label="操作" />
            </DatagridConfigurable>
          </List>
        </Grid>
      </DialogContent>
    </Dialog>
  );
}

export default ItemDialog;
