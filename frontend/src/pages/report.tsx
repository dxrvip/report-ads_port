import {
    BooleanField,
    Create,
    Datagrid,
    Edit,
    EditButton,
    List,
    SimpleForm,
    TextField,
    TextInput,
  } from "react-admin";
import { SubjectField } from "../components/SubjectField";
  
  export const ReportList = (props: any) => (
    <List {...props} filters={[]}>
      <Datagrid>
        <TextField source="id" />
        <TextField source="url" sx={{width: "50px", height: "20px", display: "inline-block", overflow: "hidden"}} />
        <TextField source="post.slug" />
        <TextField source="UV" />
        <TextField source="PV" />
        <TextField source="ads点击数" />
        <TextField source="是否屏蔽" />
        {/* <BooleanField source="is_page" /> */}
        <EditButton label="操作" />
      </Datagrid>
    </List>
  );
  
  export const ReportEdit = (props: any) => (
    <Edit {...props}>
      <SimpleForm>
        <TextInput source="url" />
      </SimpleForm>
    </Edit>
  );
  
  export const ReportCreate = (props: any) => (
    <Create {...props}>
      <SimpleForm>
        <TextInput source="url" />
      </SimpleForm>
    </Create>
  );
  