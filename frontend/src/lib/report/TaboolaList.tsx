import {
    List,
    Datagrid,
    TextField,
    useGetRecordId,
    DateField
  } from "react-admin";
import { CaceZsField } from "../../components/SimpleDialog";
// import InvoiceShow from "./InvoiceShow";
  
  const TaboolaList = (props: any) => {
    const recordId = useGetRecordId();
  
    return (
        <List resource="list/taboola" actions={false} filter={{ domain_id: recordId }} title="/特博拉">
          <Datagrid >
            <TextField source="id" />
            <TextField source="site_id" label="siteId" />
            <DateField source="create" label="时间" showTime />
            <TextField source="page_sum" label="翻页深度" />
            {/* <CaceZsField source="zs_sum" label="纵深" /> */}
            <TextField source="post_sum" label="总文章数" />
            <TextField source="ip_sum" label="总访客数" />
            <TextField source="report_sum" label="累计浏览量" />
          </Datagrid>
        </List>
    );
  };
  
  export default TaboolaList;
  