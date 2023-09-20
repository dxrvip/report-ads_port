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
          <MyButton source="taboola_sum" label="siteId" />
          {/* <TextField source="page_sum" label="翻页数" /> */}
          <TextField source="zssum" label="有纵深行为访客数" />
          <TextField source="ip_sum" label="访客总数" />
          <TextField source="report_sum" label="累计浏览量" />
          <SendTaboolaAdsStates label="操作" />
        </Datagrid>
      </List>
  );
};

export default PostList;
