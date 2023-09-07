import {
  Edit,
  SimpleForm,
  TextInput,
} from "react-admin";

function DomainEdit(props: any) {
  return (<Edit {...props}>
    <SimpleForm>
      <TextInput source="base_url" />
    </SimpleForm>
  </Edit>)
}

export default DomainEdit;
