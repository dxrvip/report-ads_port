import { Card, CardContent, Grid, Typography } from "@mui/material";
import {
  Datagrid,
  DateField,
  List,
  TextField,
  useRecordContext,
} from "react-admin";
import { Invoice } from "../../types";
import CustomerField from "../../components/ShowRecharts";

export interface TypeUrl {
  type?: string;
  record: Invoice;
}

const ShowHeard = ({ type, record }: TypeUrl) => {
  if (type == "taboola")
    return (
      <>
        siteId:
        <a style={{ marginLeft: "4px" }} href={record.url}>
          {record.site_id}
        </a>
      </>
    );
  if (type == "post")
    return (
      <>
        url:
        <a style={{ marginLeft: "4px" }} href={record.url}>
          {record.url}
        </a>
      </>
    );

  return <></>;
};

const InvoiceShow = (props: any) => {
  const record = useRecordContext<Invoice>();

  if (!record) return null;

  return (
    <Card sx={{ width: "98%", margin: "auto" }}>
      <CardContent>
        <Grid container spacing={2}>
          <Grid item xs={12} ml={6}>
            <Typography gutterBottom>
              Id: <span style={{ color: "red" }}>{record.id}</span> -
              <ShowHeard type={props?.type} record={record} />
            </Typography>
          </Grid>

          <CustomerField type={props?.type} />
          <Grid item ml={6}>
            <List
              resource="list/taboola"
              actions={false}
              filter={{ record_id: record.id }}
              title="/特博拉"
            >
              <Datagrid>
                <TextField source="id" />
                <TextField source="site_id" label="siteId" />
                <DateField source="create" label="时间" showTime />
                <TextField source="platform" label="设备" />
                <TextField source="psum" label="总文章数" />
                <TextField source="bsum" label="总访客数" />
                <TextField source="rsum" label="累计浏览量" />
              </Datagrid>
            </List>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default InvoiceShow;
