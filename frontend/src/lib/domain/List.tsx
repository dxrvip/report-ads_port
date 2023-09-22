import {
  Datagrid,
  EditButton,
  Identifier,
  List,
  RaRecord,
  UrlField,
  DateField,
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
      <Datagrid rowClick={postRowClick as any}>
        <TextField source="id" label="ID" />
        <UrlField source="base_url" label="推广网址" />
        <DateField source="create" label="添加时间" />
        <TextField source="post_sum" label="推广文章数" />
        <TextField source="bsum" label="访客数" />
        <TextField source="rsum" label="浏览量" />
        <TextField source="tsum" label="Taboola数" />
        <EditButton label="操作" />
      </Datagrid>
    </List>
  );
};

export default DomainList;
