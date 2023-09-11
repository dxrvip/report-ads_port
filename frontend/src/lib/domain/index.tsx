import DomainCreate from "./Create";
import BlurLinearIcon from "@mui/icons-material/BlurLinear";
import DomainEdit from "./Edit";
import DomainList from "./List";
import DomainShow from './Show'

const domain = {
  edit: DomainEdit,
  create: DomainCreate,
  list: DomainList,
  show: DomainShow,
  icon: BlurLinearIcon,
  options: { label: "推广网址" },
};

export default domain;
