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
    redirect(`${id}/show`);
    return false;
  };
  return (
    <List {...props}>
      <Datagrid
        optimized
        rowClick={postRowClick as any}
        sx={{
          "& .RaDatagrid-thead": {
            backgroundColor: "red",
            color: "red"
          },
        }}
      >
        <TextField source="id" label="ID" />
        <UrlField source="base_url" label="推广网址" />
        <DateField source="create" label="添加时间" />
        <TextField source="taboola_count" label="Site_Id数" />
        <TextField source="post_count" label="推广文章数" />
        <TextField source="browser_count" label="指纹访客数" />
        <TextField source="ip_count" label="iP访客数" />
        <TextField source="report_count" label="浏览量" />
        <EditButton label="操作" />
      </Datagrid>
    </List>
  );
};

export default DomainList;
