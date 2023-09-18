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

const PostList = (props: any) => {
  const recordId = useGetRecordId();

  return (
      <List
        resource="list/post"
        actions={false}
        filter={{ record_id: recordId }}
        title="/文章"
        debounce={1000}
          >
        <Datagrid rowClick="expand" expand={<InvoiceShow type="post" />} >
          <TextField source="id" />
          <MyUrlField source="url" />
          <DateField source="create_time" label="添加日期" showTime />
          <TextField source="tsum" label="siteId" />
          <TextField source="zssum" label="有纵深行为访客数" />
          <TextField source="bsum" label="访客总数" />
          <TextField source="rsum" label="访问页面总数" />
          <SendTaboolaAdsStates label="操作" />
        </Datagrid>
      </List>
  );
};

export default PostList;
