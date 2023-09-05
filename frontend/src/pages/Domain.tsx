import {
  Create,
  Datagrid,
  Edit,
  EditButton,
  List,
  SimpleForm,
  TextField,
  TextInput,
} from "react-admin";

export const DomainList = (props: any) => (
  <List {...props} filters={[]}>
    <Datagrid>
      <TextField source="id" label="ID" />
      <TextField source="base_url" label="网址" />
      <EditButton label="操作" />
    </Datagrid>
  </List>
);

export const DomainEdit = (props: any) => (
  <Edit {...props}>
    <SimpleForm>
      <TextInput source="base_url" />
    </SimpleForm>
  </Edit>
);

export const DomainCreate = (props: any) => (
  <Create {...props}>
    <SimpleForm>
      <TextInput source="base_url" label="http://..."  />
    </SimpleForm>
  </Create>
);
