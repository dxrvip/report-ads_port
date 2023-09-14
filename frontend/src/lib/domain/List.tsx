import {
  Datagrid,
  EditButton,
  Identifier,
  List,
  RaRecord,
  TextField,
  useRedirect,
} from "react-admin";
interface RowClick {
  (id?: Identifier, resource?: string, record?: RaRecord): boolean;
}

const DomainList = (props: any) => {
  const redirect = useRedirect();
  const postRowClick: RowClick = function (id) {
    redirect(`${id}/show`)
    return false;
  };
  return (
    <List {...props} filters={[]}>
      <Datagrid rowClick={'show'}>
        <TextField source="id" label="ID" />
        <TextField source="base_url" label="网址" />
        <TextField source="sum_posts[0]" label="推广文章数" />
        <TextField source="sum_posts[1]" label="访客数" />
        <TextField source="sum_posts[2]" label="浏览量" />
        <EditButton label="操作" />
      </Datagrid>
    </List>
  );
};

export default DomainList;
