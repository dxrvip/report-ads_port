import {
  List,
  Datagrid,
  TextField,
  useGetRecordId,
  DateField,
} from "react-admin";
import SendTaboolaAdsStates from "../../components/SendTaboolaAdsStates";
// import InvoiceShow from "./InvoiceShow";

const TaboolaList = (props: any) => {
  const recordId = useGetRecordId();

  return (
    <List
      resource="list/taboola"
      actions={false}
      filter={{ domain_id: recordId }}
      title="/特博拉"
    >
      <Datagrid>
        <TextField source="id" />
        <TextField source="site_id" label="siteId" />
        <TextField source="site" label="平台名称" />
        <DateField source="create" label="时间" showTime />
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
  );
};

export default TaboolaList;
