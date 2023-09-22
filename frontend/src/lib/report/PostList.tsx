import {
  List,
  Datagrid,
  TextField,
  DateField,
  useGetRecordId,
} from "react-admin";
import InvoiceShow from "./InvoiceShow";
import MyUrlField from "../../components/MyUrlFile";
import SendTaboolaAdsStates from "../../components/SendPostAdsStates";
import MyButton from "../../components/MyButton";

const PostList = (props: any) => {
  const recordId = useGetRecordId();

  return (
      <List
        resource="list/post"
        actions={false}
        filter={{"domain_id": recordId}}
        title="/文章"
        debounce={200}
          >
        <Datagrid rowClick="expand" expand={<InvoiceShow type="post" />} >
          <TextField source="id" />
          <MyUrlField source="url" />
          <DateField source="create_time" label="添加日期" showTime />
          <MyButton source="taboola_count" label="siteId总数" />
          <MyButton source="tab_open_sum" label="siteId进入数" />
          <TextField source="page_sum" label="翻页总数" />
          <TextField source="zs_sum" label="有纵深行为访客数" />
          <TextField source="ip_count" label="Ip访客总数" />
          <TextField source="borwser_count" label="指纹访客总数" />
          <TextField source="report_count" label="累计浏览量" />
          <SendTaboolaAdsStates label="操作" />
        </Datagrid>
      </List>
  );
};

export default PostList;
