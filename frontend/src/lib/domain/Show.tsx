import {
  // TextField,
  // List,
  // Datagrid,
  ShowView,
} from "react-admin";
// import Dialog from "@mui/material/Dialog";
// import DialogTitle from "@mui/material/DialogTitle";
// import { useParams } from "react-router-dom";
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";
import Paper from "@mui/material/Paper";
import PostList from "../report/PostList";
import TaboolaList from "../report/TaboolaList";
import React from "react";
import TabPanel from "../../components/TabPanel";
import BrowserList from "../report/BrowserList";
import ReportList from "../report/ReportList";

// function SimpleDialog(props: any) {
//   const { onClose, selectedValue, open } = props;

//   const handleClose = () => {
//     onClose(selectedValue);
//   };

//   return (
//     <Dialog
//       onClose={handleClose}
//       aria-labelledby="simple-dialog-title"
//       open={open}
//     >
//       <DialogTitle id="simple-dialog-title">Set backup account</DialogTitle>
//       <List>
//         <Datagrid>
//           <TextField source="id" />
//           <TextField source="base_url" />
//         </Datagrid>
//       </List>
//     </Dialog>
//   );
// }

const DomainShow = (props: any) => {
  // const { id } = useParams();
  const [value, setValue] = React.useState(0);
  const handleChange = (event: React.ChangeEvent<{}>, newValue: number) => {
    setValue(newValue);
  };
  return (
    <ShowView actions={false} title="数据明细">
      <Paper className="">
        <Tabs
          value={value}
          onChange={handleChange}
          indicatorColor="primary"
          textColor="primary"
        >
          <Tab label="文章列表" />
          <Tab label="Taboola List" />
          <Tab label="指纹列表" />
          <Tab label="访问记录" />
        </Tabs>
      </Paper>
      <TabPanel value={value} index={0}>
        <PostList />
      </TabPanel>
      <TabPanel value={value} index={1}>
        <TaboolaList />
      </TabPanel>
      <TabPanel value={value} index={2}>
        <BrowserList />
      </TabPanel>
      <TabPanel value={value} index={3}>
        <ReportList />
      </TabPanel>
    </ShowView>
    // </>
  );
};

export default DomainShow;
