import { Card, CardContent, Grid } from "@mui/material";
import {
  TextField,
  List,
  useRecordContext,
  DatagridConfigurable,
} from "react-admin";
import { Invoice } from "../../types";
import CustomerField from "../../components/ShowRecharts";

export interface TypeUrl {
  type?: string;
  record: Invoice;
}

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
