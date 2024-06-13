import React, { useState } from "react";
import { Field, Form, Formik } from "formik";
import * as yup from "yup";
import {
  Box,
  Button,
  FormControl,
  FormErrorMessage,
  Input,
  InputGroup,
  InputLeftElement,
  InputRightElement,
  Link,
  Stack,
  Text,
} from "@chakra-ui/react";
import { EmailIcon, LockIcon, ViewIcon, ViewOffIcon } from "@chakra-ui/icons";
const Login = () => {
  const [showPassword, setShowPassword] = useState(false);

  const handleTogglePassword = () => {
    setShowPassword((prev) => !prev);
  };

  const initialValues = {
    email: "",
    password: "",
  };

  const loginSchema = yup.object().shape({
    email: yup
      .string()
      .email("Please enter a valid email address")
      .required("This field is required"),

    password: yup
      .string()
      .required("Password is required")
      .min(8, "Password must be atleast 8 characters long"),
  });

  const handleSubmit = async (values, { isSubmitting }) => {
    try {
      const response = await login({
        email: values.email,
        password: values.password,
      });
      if (response.error) {
        const errorMessage = response.error.message || "Login failed";
        toast(errorMessage);
        return;
      }
    } catch (error) {
      console.error("An expected error occured.Please try again later", error);
    }
  };

  return (
    <Box
      minH={"100vh"}
      w={{ base: "100%", md: "50%" }}
      className="h-screen w-full py-[60px] flex flex-col justify-center items-center"
    >
      <Text className="mb-10 font-semibold font-montserrat text-[#33658a] text-4xl">
        Sign in
      </Text>

      <Formik
        initialValues={initialValues}
        validationSchema={loginSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting }) => (
          <Form className=" ">
            <Stack direction={"column"} spacing={8}>
              <>
                <Field name="email">
                  {({ field, form }) => (
                    <FormControl
                      isInvalid={form.errors.email && form.touched.email}
                    >
                      <InputGroup>
                        <InputLeftElement pointerEvents="none">
                          <EmailIcon color="gray.400" />
                        </InputLeftElement>
                        <Input
                          errorBorderColor="crimson"
                          focusBorderColor={"#33658a"}
                          placeholder="Email"
                          {...field}
                        />
                      </InputGroup>
                      <FormErrorMessage color="crimson">
                        {form.errors.email &&
                          form.touched.email &&
                          form.errors.email}
                      </FormErrorMessage>
                    </FormControl>
                  )}
                </Field>
                <Field name="password">
                  {({ field, form }) => (
                    <FormControl
                      isInvalid={form.errors.password && form.touched.password}
                    >
                      <InputGroup>
                        <InputLeftElement pointerEvents="none">
                          <LockIcon color="gray.400" />
                        </InputLeftElement>
                        <Input
                          errorBorderColor="crimson"
                          focusBorderColor={"#33658a"}
                          placeholder="Password"
                          {...field}
                          type={showPassword ? "text" : "password"}
                        />
                        <InputRightElement width="4.5rem">
                          <Box
                            h="1.75rem"
                            size="sm"
                            onClick={handleTogglePassword}
                          >
                            {showPassword ? <ViewOffIcon /> : <ViewIcon />}
                          </Box>
                        </InputRightElement>
                      </InputGroup>
                      <FormErrorMessage color="crimson">
                        {form.errors.password &&
                          form.touched.password &&
                          form.errors.password}
                      </FormErrorMessage>
                    </FormControl>
                  )}
                </Field>
              </>

              <Button
                alignSelf={"center"}
                w={"150px"}
                bg={"#33658a"}
                color={"#fff"}
                type="submit"
                variant={"ghost"}
                _hover={{ boxShadow: "dark-lg" }}
                isLoading={isSubmitting}
                fontFamily={"montserrat"}
              >
                Sign In
              </Button>
              <Box fontSize="sm" className="mx-auto">
                <Text fontFamily={"montserrat"}>
                  Don't have an account? &nbsp;
                  <Link to="/SignUp">
                    <span className="font-montserrat hover:text-[#33658a]">
                      Sign Up
                    </span>
                  </Link>
                </Text>
              </Box>
            </Stack>
          </Form>
        )}
      </Formik>
      {/* <button  className="px-6 py-3 flex text-red-700 font-bold" onClick={()=> navigate('/')}>
          <IoChevronBack fontSize={'1.3rem'}/>Back
        </button> */}
    </Box>
  );
};

export default Login;
