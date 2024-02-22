import theme from '../theme';
import ResponsiveAppBar from './navbar';

function Layout(props: any) {
    return (
      <div className="page-layout">
        <ResponsiveAppBar></ResponsiveAppBar>
        {props.children}
        <style jsx global>{`
        body {
          background: ${theme.palette.primary};
        }
        #
      `}</style>
      </div>
    );
  }
   
export default Layout;