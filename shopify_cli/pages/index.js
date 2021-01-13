import { EmptyState, Layout,Card,Stack, Page,Form,FormLayout,TextStyle,Button, TextField,ChoiceList,Select } from '@shopify/polaris';
import { ResourcePicker, TitleBar } from '@shopify/app-bridge-react';
import React, {useCallback, useState, Component, PureComponent} from 'react';
import axios from 'axios';
// require('dotenv').config({ path:path.resolve(__dirname, '../.env') })


class Index extends React.Component {
  state = { 
    open: false,
    website: "",
    url: "",
    intent: "none",
    amount:"0",
    prodid: {},
    time: "3600",
    max: "10000",
    min: "0",
  };
    render() {
      const { website } = this.state;
      const { url } = this.state;
      const { intent } = this.state;
      const { amount } = this.state;
      const { time } = this.state;
      const { max } = this.state;
      const { min } = this.state;


      return (
    <Page>
        <TitleBar
        title="Price tracking and automation"
        primaryAction={{
          content: 'Select products',
          onAction: () => this.setState({ open: true }),
        }}
      />
      <ResourcePicker
            resourceType="Product"
            showVariants={false}
            open={this.state.open}
            onSelection={(resources) => this.handleSelection(resources)}
            onCancel={() => this.setState({ open: false })}
          />
      <Layout>
        {/* <TextStyle variation="strong" >
        Amazon Price Tracker
      </TextStyle> */}
      <EmptyState
          heading="Always remain competitive by automating the price"
          action={{
            content: 'Select Product',
            onAction: () => this.setState({ open: true }),
          }}
        >
          <ResourcePicker
            resourceType="Product"
            showVariants={false}
            open={this.state.open}
            onSelection={(resources) => this.handleSelection(resources)}
            onCancel={() => this.setState({ open: false })}
          />
          <p>Fill out the necessary fields given below. </p>
        </EmptyState>
        {/* <Card > */}
              <Form noValidate onSubmit={this.handleSubmit}>
                <FormLayout>
                  <p>Choose Ecom website</p>
                <Select
                    // title="Choose Ecom website"
                    options={[
                      {label: 'Amazon', value: 'amazon'},
                      {label: 'Snapdeal', value: 'snapdeal'},
                      {label: 'Flipkart', value: 'flipkart'},
                    ]}
                    value={website}
                    onChange={this.handleChange('website')}
                  />
                  <TextField
                    value={url}
                    onChange={this.handleChange('url')}
                    label="URL of the product page"
                    type="url"
                  />
                  <ChoiceList
                    title="How you want to set the price with respct to above product"
                    choices={[
                      {label: 'Same', value: 'same'},
                      {label: 'Less By', value: 'less'},
                      {label: 'More By', value: 'more'},
                    ]}
                    selected={intent}
                    onChange={this.handleChange('intent')}
                  />
                   <TextField
                    value={amount}
                    onChange={this.handleChange('amount')}
                    label="Amount"
                  />
                  <h4> Price boundaries</h4>
                   <TextField
                    value={max}
                    onChange={this.handleChange('max')}
                    label="Maximum price"
                  />
                   <TextField
                    value={min}
                    onChange={this.handleChange('min')}
                    label="Minimum price"
                  />
                   <TextField
                    value={time}
                    onChange={this.handleChange('time')}
                    label="Check after(Entered value will be considered in seconds)"
                  />
                 
                  <Stack distribution="trailing">
                    <Button primary submit>
                      Save
                    </Button>
                  </Stack>
                </FormLayout>
              </Form>
            {/* </Card> */}
      </Layout>
      </Page>
    );
    
  }
  handleSelection = (resources) => {
    const productid = resources.selection.map((product) => product.id);
    this.setState({ open: false })
    this.setState({ prodid:productid })
  };


  handleSubmit = () => {


    this.setState({
      website: this.state.website,
      url: this.state.url,
      intent: this.state.intent,
      amount: this.state.amount,
      prodid : this.state.prodid,
      max : this.state.max,
      min : this.state.min,
    });
    console.log('submission', this.state);
    console.log(JSON.stringify(this.state))
    
  var myParams1 = {
    "website":this.state.website,
    "url": this.state.url,
    "intent": this.state.intent,
    "amount": this.state.amount,
    "prodid" : this.state.prodid,
    "time" : this.state.time,
    "max" : this.state.max,
    "min" : this.state.min,
    "shop" : window.location.href,
  }
  var responsedata

  axios.post('http://127.0.0.1:5000/result', myParams1)

  .then(function (response) {

  console.log(response)
  responsedata = response
  console.log(JSON.stringify(responsedata))

  })
  };

  handleChange = (field) => {
    return (value) => this.setState({ [field]: value });
  };

}



export default Index;