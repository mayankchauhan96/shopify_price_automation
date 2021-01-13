import React, { Component } from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';
import { EmptyState, Layout,Card,Frame,Loading, Page,Form,FormLayout,TextStyle,Button, TextField,ChoiceList,DataTable } from '@shopify/polaris';
import { ResourcePicker, TitleBar } from '@shopify/app-bridge-react';


class data extends Component {
  state = { 
    open: false,
    prodid: {},
  };
//   constructor(props) {
//     super(props);
//     this.state = {
//       items: [],
//       isLoaded: false,
//     };
//   }
  componentDidMount() {
    

  }
  render() {

      return (
       
        <Page title="Terminate service">
          <ResourcePicker
            resourceType="Product"
            showVariants={false}
            open={this.state.open}
            onSelection={(resources) => this.handleSelection(resources)}
            onCancel={() => this.setState({ open: false })}
          />
          <EmptyState
          heading="Please select the product to stop the price automation"
          action={{
            content: 'Select Product',
            onAction: () => this.setState({ open: true }),
          }}
        ></EmptyState>
        
      </Page>

       
      );
    }
  
  handleSelection = (resources) => {
    const productid = resources.selection.map((product) => product.id);
    this.setState({ open: false })
    this.setState({ prodid:productid })
    var params = {
        "prodid" : this.state.prodid,
      }
  
      axios.post("http://127.0.0.1:5000/terminate", params)
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
  };

}
export default data;