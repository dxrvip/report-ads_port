// import {
//   // TextField,
//   // List,
//   // Datagrid,
//   ShowView,
// } from "react-admin";
import { Tab, Tabs, Card } from "@mui/material";
import PostList from "../report/PostList";
import TaboolaList from "../report/TaboolaList";
import React from "react";
import TabPanel from "../../components/TabPanel";
import ReportList from "../report/ReportList";

function a11yProps(index: any) {
  return {
    id: `simple-tab-${index}`,
    "aria-controls": `simple-tabpanel-${index}`,
  };
}
const DomainShow = (props: any) => {
  // const { id } = useParams();
  const [value, setValue] = React.useState(0);
  const handleChange = (event: React.ChangeEvent<{}>, newValue: number) => {
      setValue(newValue);

  };
  return (
    <Card title="数据明细">
      <Tabs
        value={value}
        onChange={handleChange}
        indicatorColor="primary"
        textColor="primary"
        aria-label="simple tabs example"
      >
        <Tab label="文章列表" {...a11yProps(0)} />
        <Tab label="SiteId列表" {...a11yProps(1)} />
        {/* <Tab label="指纹列表" {...a11yProps(2)} /> */}
        <Tab label="访问记录" {...a11yProps(2)} />
      </Tabs>
      <TabPanel value={value} index={0}>
        <PostList />
      </TabPanel>
      <TabPanel value={value} index={1}>
        <TaboolaList />
      </TabPanel>
      {/* <TabPanel value={value} index={2}>
        <BrowserList />
      </TabPanel> */}
      <TabPanel value={value} index={2}>
        <ReportList />
      </TabPanel>
    </Card>
  );
};

export default DomainShow;
