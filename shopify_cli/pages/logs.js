import React, { Component } from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';
import { EmptyState, Layout,Card,Frame,Loading, Page,Form,FormLayout,TextStyle,Button, TextField,ChoiceList,DataTable } from '@shopify/polaris';
import { ResourcePicker, TitleBar } from '@shopify/app-bridge-react';


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

    axios.post("http://127.0.0.1:5000/data", params)
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
       
        <Page title="Price change History">
        <Card>
          <DataTable
            columnContentTypes={[
              'numeric',
              "time",
              'text',
              'text',
              'text',
              'text',
              'text',
              'text',
              'text',
              'numeric',
              'text',
              'numeric',
              'text',
              'text',

            ]}
            headings={[
              'Try No.',
              "Time Stamp",
              "Compared to",
              "Price Update Status", 
              "Compared product name",
              "Url",
              "Product name",
              "Variant Id",
              "Email Alert",
              "Amazon price",
              "Intent",
              "Price difference",
              "Store's current price",
              "Store's updated price"
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