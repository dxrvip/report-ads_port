import {
  List,
  TextField,
  useGetRecordId,
  DateField,
  TextInput,
  DateInput,
  BooleanInput,
  TopToolbar,
  SelectColumnsButton,
  FilterButton,
  DatagridConfigurable,
} from "react-admin";
import SendTaboolaAdsStates from "../../components/SendTaboolaAdsStates";
import MyTextField from "../../components/MyTextFile";
import MyStatusField from "../../components/MyStatusField";
// import InvoiceShow from "./InvoiceShow";
const taboolaFilters = [
  <TextInput label="搜索：ID" source="id"  />,
  <TextInput label="搜索：SITE_ID" source="site_id"  />,
  <DateInput label="添加日期" source="create"  />,
  <BooleanInput label="推广状态" source="promotion"  />,
];

const ListActions = () => (
  <TopToolbar>
    <SelectColumnsButton />
    <FilterButton />
  </TopToolbar>
);


const TaboolaList = (props: any) => {
  const recordId = useGetRecordId();

  return (
    <List
      resource="list/taboola"
      disableSyncWithLocation
      storeKey={false}
      actions={<ListActions />}
      exporter={false}
      filter={{ domain_id: recordId }}
      filters={taboolaFilters}
      title="/特博拉"
    >
      <DatagridConfigurable>
        <TextField source="id" />
        <TextField source="site_id" label="siteId" />
        <TextField source="hs_sum" label="机房ip数" />
        <MyTextField source="site" label="平台名称" />
        <DateField source="create" label="时间" showTime />
        <TextField source="page_sum" label="翻页数" />
        <TextField source="zs_sum" label="有纵深行为访客数" />
        <TextField source="ads_count" label="广告点击数" />
        <TextField source="ip_count" label="Ip访客数" />
        <TextField source="tab_open_sum" label="siteId进入数" />
        <TextField source="borwser_count" label="指纹访客数" />
        <TextField source="report_count" label="总浏览量" />
        <MyStatusField source="promotion" label="状态" />
        <SendTaboolaAdsStates label="操作" />
      </DatagridConfigurable>
    </List>
  );
};

export default TaboolaList;
