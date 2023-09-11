import {
    List,
    Datagrid,
    TextField,
    DateField,
    useGetRecordId,
  } from "react-admin";
  
  const BrowserList = (props: any) => {
    const recordId = useGetRecordId();
  
    return (
      <div>
        <List resource="list/browser" actions={false} filter={{ record_id: recordId }}>
          <Datagrid>
            <TextField source="id" />
            <TextField source="user_agent" label="user_agent" />
            <DateField source="update_time" label="时间" />
            <TextField source="psum" label="文章数" />
            <TextField source="rsum" label="浏览量" />
          </Datagrid>
        </List>
      </div>
    );
  };
  
  export default BrowserList;
  