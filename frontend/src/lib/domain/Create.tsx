import {
    Create,
    SimpleForm,
    TextInput,
  } from "react-admin";


const DomainCreate = ({props}: any) => (
    <Create {...props}>
    <SimpleForm>
      <TextInput source="base_url" label="http://..."  />
    </SimpleForm>
  </Create>
)

export default DomainCreate;