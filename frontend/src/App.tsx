import { createBrowserHistory as createHistory } from "history";
import simpleRestProvider from "ra-data-simple-rest";
import { Admin, fetchUtils, Resource, CustomRoutes } from "react-admin";
import { Route } from "react-router";
import MyLayout from "./components/AdminLayout";
import Dashboard from "./pages/Dashboard";
// import { ItemCreate, ItemEdit, ItemList } from "./pages/Items";
import report from "./lib/report";
import LoginPage from "./pages/Login";
import { ProfileEdit } from "./pages/ProfileEdit";
import Register from "./pages/Register";
import { UserEdit, UserList } from "./pages/Users";
import authProvider from "./providers/authProvider";
import { basePath } from "./providers/env";
import PersonIcon from "@mui/icons-material/Person";
import domain from "./lib/domain"

const httpClient = (url: string, options: any = {}) => {
  options.user = {
    authenticated: true,
    token: `Bearer ${localStorage.getItem("token")}`,
  };
  if (url.includes("/users/") && options.method === "PUT") {
    // 我们使用PATCH在后端为用户进行更新，因为PATCH是选择性PUT，所以这个更改应该没问题
    options.method = "PATCH";
  }
  return fetchUtils.fetchJson(url, options);
};

const dataProvider = simpleRestProvider(`${basePath}/api/v1`, httpClient);

const App = () => {
  return (
    <Admin
      disableTelemetry
      dataProvider={dataProvider}
      authProvider={authProvider}
      loginPage={LoginPage}
      history={createHistory()}
      layout={MyLayout}
      dashboard={Dashboard}
    >
      <CustomRoutes>
        <Route path="/my-profile" element={<ProfileEdit />} />
      </CustomRoutes>
      <CustomRoutes noLayout>
        <Route path="/register" element={<Register />} />
      </CustomRoutes>
      {(permissions) => [
        permissions.is_superuser === true ? (
          <Resource
            options={{ label: "Users" }}
            name="users"
            list={UserList}
            edit={UserEdit}
            icon={PersonIcon}
          />
        ) : null,
        <Resource name="domain" {...domain}/>,
        // <Resource name="report" {...report}/>,
      ]}
    </Admin>
  );
};

export default App;
