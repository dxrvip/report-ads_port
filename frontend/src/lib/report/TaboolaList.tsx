import {
    List,
    Datagrid,
    TextField,
    useGetRecordId,
  } from "react-admin";
import InvoiceShow from "./InvoiceShow";
  
  const TaboolaList = (props: any) => {
    const recordId = useGetRecordId();
  
    return (
      <div>
        <List resource="list/taboola" actions={false} filter={{ record_id: recordId }} title="/特博拉">
          <Datagrid rowClick="expand" expand={<InvoiceShow type="taboola" />}>
            <TextField source="id" />
            <TextField source="site_id" label="siteId" />
            <TextField source="platform" label="设备" />
            <TextField source="psum" label="文章数" />
            <TextField source="psum" label="访客数" />
            <TextField source="rsum" label="浏览量" />
          </Datagrid>
        </List>
      </div>
    );
  };
  
  export default TaboolaList;
  