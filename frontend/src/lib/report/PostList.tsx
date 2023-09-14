import {
  List,
  Datagrid,
  TextField,
  useGetRecordId,
} from "react-admin";
import InvoiceShow from "./InvoiceShow";

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
          <TextField source="id"/>
          <TextField source="url" label="Url" />
          <TextField source="tsum" label="Tab计数" />
          <TextField source="bsum" label="访客数" />
          <TextField source="rsum" label="浏览量" />
        </Datagrid>
      </List>
  );
};

export default PostList;
