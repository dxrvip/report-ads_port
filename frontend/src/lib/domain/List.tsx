import {
    Datagrid,
    EditButton,
    List,
    TextField,
  } from "react-admin";


const DomainList = (props: any) => (
    <List {...props} filters={[]}>
    <Datagrid>
      <TextField source="id" label="ID" />
      <TextField source="base_url" label="网址" />
      <TextField source="sum_posts[0]" label="推广文章数" />
      <TextField source="sum_posts[1]" label="访客数" />
      <TextField source="sum_posts[2]" label="浏览量" />
      <EditButton label="操作" />
    </Datagrid>
  </List>
)

export default DomainList;