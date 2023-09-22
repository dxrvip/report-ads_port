import { Card, CardContent, Grid, Typography } from "@mui/material";
import { useRecordContext } from "react-admin";
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
          <Grid item pb={8}>
            <CustomerField type={props?.type} />
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default InvoiceShow;
