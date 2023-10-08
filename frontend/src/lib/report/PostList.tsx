import {
  List,
  TextField,
  DateField,
  useGetRecordId,
  TextInput,
  DateInput,
  BooleanInput,
  SelectColumnsButton,
  TopToolbar,
  FilterButton,
  DatagridConfigurable,
} from "react-admin";
import InvoiceShow from "./InvoiceShow";
import MyUrlField from "../../components/MyUrlFile";
import MyButton from "../../components/MyButton";
import MyFloatField from "../../components/MyFloatField";
import MyItemStatusField from "../../components/MyItemStatusField";

const postFilters = [
  <TextInput label="搜索：ID" source="id" />,
  <TextInput label="搜索：SLUG" source="slug" />,
  <DateInput label="日期筛选" source="create_time" alwaysOn />,
  // <BooleanInput label="推广状态" source="promotion" />,
];

const ListActions = () => (
  <TopToolbar>
    <SelectColumnsButton />
    <FilterButton />
  </TopToolbar>
);

const PostList = (props: any) => {
  const recordId = useGetRecordId();

  return (
    <List
      resource="list/post"
      actions={<ListActions />}
      storeKey={false}
      exporter={false}
      filter={{ domain_id: recordId }}
      filters={postFilters}
      title="/文章"
      debounce={200}
      disableSyncWithLocation
    >
      <DatagridConfigurable rowClick="expand" expand={<InvoiceShow type="post" />}>

          <TextField source="id" />
          <MyUrlField source="url" />
          {/* <DateField source="create_time" label="添加日期" showTime /> */}
          <MyButton source="taboola_count" label="siteId总数" />
          <TextField source="page_sum" label="翻页总数" />
          <TextField source="zs_sum" label="有纵深行为访客数" />
          <MyFloatField
            source="page_zs"
            label="翻页/site进入数"
            reference={4}
          />
          <TextField source="ads_count" label="广告点击数" />
          <TextField source="ip_count" label="Ip访客总数" />
          <TextField source="tab_open_sum" label="siteId进入数" />
          <MyFloatField
            source="zs_site_open"
            label="纵深/site进入数"
            reference={0.3}
          />
          <TextField source="borwser_count" label="指纹访客总数" />
          <TextField source="report_count" label="累计浏览量" />
          <TextField source="ads_show_sum" label="广告显示计数" />
          
          {/* <MyStatusField source="promotion" label="状态" /> */}
          <MyItemStatusField source="promotion" label="推广状态"  />
          {/* <SendTaboolaAdsStates label="操作" /> */}
      </DatagridConfigurable>
    </List>
  );
};

export default PostList;
