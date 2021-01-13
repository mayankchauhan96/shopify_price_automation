import React, { Component } from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';
import { EmptyState, Layout,Card,Frame,Loading, Page,Form,FormLayout,TextStyle,Button, TextField,ChoiceList,DataTable } from '@shopify/polaris';


class data extends Component {
  constructor(props) {
    super(props);
    this.state = {
      items: [],
      isLoaded: false,
    };
  }
  componentDidMount() {
    var params = {
      "shop" : window.location.href,
    }

    axios.post("http://127.0.0.1:5000/isactive", params)
    .then( (response) => {
      var resdata;
  
      resdata = response;
      // console.log(response)
      console.log(resdata);
      this.setState({
        isLoaded: true,
        items: resdata.data.data,
      });
    });

  }
  render() {
    var { isLoaded, items } = this.state;
    if (!isLoaded) {
      return <div style={{height: '100px'}}>
      <Frame>
        <Loading />
      </Frame>
    </div>
    } else {
      return (
       
        <Page title="Products that are running on Price automation">
        <Card>
          <DataTable
            columnContentTypes={[
              'text',
              'text',
              'text',
              'link',


            ]}
            headings={[
              "Product ID",
              "Product name",
              "compared to",
              "URL of compared product"
            ]}
            rows={items}
          />
        </Card>
      </Page>

       
      );
    }
  }
}
export default data;