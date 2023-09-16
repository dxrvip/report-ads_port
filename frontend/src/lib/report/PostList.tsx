import {
  List,
  Datagrid,
  TextField,
  DateField,
  useGetRecordId,
} from "react-admin";
import InvoiceShow from "./InvoiceShow";
import MyUrlField from "../../components/MyUrlFile";

const PostList = (props: any) => {
  const recordId = useGetRecordId();

  return (
      <List
        resource="list/post"
        actions={false}
        filter={{ record_id: recordId }}
        title="/文章"
          >
        <Datagrid rowClick="expand" expand={<InvoiceShow type="post" />}>
          <TextField source="id" />
          <MyUrlField source="url" />
          <DateField source="create_time" label="添加日期" showTime />
          <TextField source="tsum" label="Taboola数" />
          <TextField source="bsum" label="访客数" />
          <TextField source="rsum" label="浏览量" />
        </Datagrid>
      </List>
  );
};

export default PostList;
