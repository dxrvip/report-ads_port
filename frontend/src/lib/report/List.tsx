import { Datagrid,BooleanField, List, TextField, DateField } from "react-admin";


const ReportList = (props: any) => (
  <List {...props} filters={[]}>
    <Datagrid>
      <TextField source="url" color="secondary"/>
      <DateField source="create" showTime label="日期" />
      <TextField source="browser_info.fingerprint_id" label="指纹ID" />
      <TextField source="visitor.ip" label="Ip" />
      <TextField source="browser_info.equipment.browser[0]" label="浏览器" />
      <TextField source="browser_info.equipment.os[0]" label="设备" />
      <BooleanField source="browser_info.equipment.is_bot" label="机器人" />
      <BooleanField source="is_page" label="Page" />
      <TextField source="ads点击数" label="Ads" />
    </Datagrid>
  </List>
);

export default ReportList;
