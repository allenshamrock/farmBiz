import React, { useState } from "react";
import {
  Box,
  FormControl,
  FormLabel,
  InputRightElement,
  FormErrorMessage,
  Input,
  InputGroup,
  InputLeftElement,
  Select,
  Stack,
  Button,
  Image,
  Text,
  Flex,
  Link,
} from "@chakra-ui/react";
import { FaImage } from "react-icons/fa";
import * as yup from "yup";
import { Formik, Form, Field, ErrorMessage } from "formik";
import {
  AtSignIcon,
  EmailIcon,
  LockIcon,
  ViewIcon,
  ViewOffIcon,
} from "@chakra-ui/icons";

function SignUp() {
  const [showPassword, setShowPassword] = useState(false);
  const [file, setFile] = useState(null);

  const handleTogglePassword = () => {
    setShowPassword((prev) => !prev);
  };

  const SignUpSchema = yup.object().shape({
    email: yup
      .string()
      .email("Please enter a valid email address")
      .required("This field is required"),
    username: yup
      .string()
      .label("Please enter your username")
      .min(2, "too short")
      .max(70, "too long"),
    password: yup
      .string()
      .min(8, "Password must have a minimum of 8 characters"),
    confirmPassword: yup
      .string()
      .oneOf([yup.ref("password"), null], "Password must match")
      .required("Please confrim your password"),
  });

  const initialValues = {
    email: "",
    username: "",
    password: "",
    confirmPassword: "",
    profile_picture: "image",
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.file[0];
    setFile(selectedFile);
  };

  return (
    <Box
      minH={"100vh"}
      w={{ base: "100%", md: "50%" }}
      className="h-screen  py-[60px] flex flex-col justify-center items-center "
    >
      <Formik initialValues={initialValues} validationSchema={SignUpSchema}>
        {({ isSubmitting }) => (
          <Form className=" ">
            <Stack direction={"column"} spacing={8}>
              <>
                <Field name="username">
                  {({ field, form }) => (
                    <FormControl
                      isInvalid={form.errors.username && form.touched.username}
                    >
                      <InputGroup>
                        <InputLeftElement pointerEvents="none">
                          <AtSignIcon color="gray.400" />
                        </InputLeftElement>
                        <Input
                          errorBorderColor="crimson"
                          focusBorderColor={"#33658a"}
                          placeholder="Username"
                          {...field}
                        />
                      </InputGroup>
                      <FormErrorMessage color="crimson">
                        {form.errors.username &&
                          form.touched.username &&
                          form.errors.username}
                      </FormErrorMessage>
                    </FormControl>
                  )}
                </Field>

                {/* Email Field */}
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

                {/* File input */}
                <div className="flex p-4 border-dotted border-2 rounded-full border-slate-800 my-3 justify-center align-middle h-60 w-60">
                  <label className="drop-area">
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleFileChange}
                      style={{ display: "none" }}
                    />
                    <p className="w-fit flex p-2">
                      <FaImage />
                    </p>
                    {file && (
                      <div>
                        {file.type.startsWith("image/") && (
                          <img
                            src={URL.createObjectURL(file)}
                            alt="Preview"
                            style={{ maxWidth: "100%", maxHeight: "200px" }}
                          />
                        )}
                      </div>
                    )}
                  </label>
                </div>
                {/* Password Field */}
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

                {/* Confirm Password Field */}
                <Field name="confirmPassword">
                  {({ field, form }) => (
                    <FormControl
                      isInvalid={
                        form.errors.confirmPassword &&
                        form.touched.confirmPassword
                      }
                    >
                      <InputGroup>
                        <InputLeftElement pointerEvents="none">
                          <LockIcon color="gray.400" />
                        </InputLeftElement>
                        <Input
                          errorBorderColor="crimson"
                          focusBorderColor={"#33658a"}
                          placeholder="Confirm Password"
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
                        {form.errors.confirmPassword &&
                          form.touched.confirmPassword &&
                          form.errors.confirmPassword}
                      </FormErrorMessage>
                    </FormControl>
                  )}
                </Field>
              </>

              {/* Sign In Link */}

              {/* Submit Button */}
              <Button
                alignSelf={"center"}
                w={"150px"}
                bg={"#33658a"}
                color={"#ffff"}
                type="submit"
                variant={"ghost"}
                _hover={{ background: "#33658a" }}
                isLoading={isSubmitting}
                boxShadow={"dark-lg"}
                fontFamily={"raleway"}
              >
                Sign up
              </Button>
              <Box className="mx-auto font-raleway">
                <Text>
                  Already have an account?{" "}
                  <Link to="/SignIn">
                    <span className="hover:text-[#33658a]">Sign In</span>
                  </Link>
                </Text>
              </Box>
            </Stack>
          </Form>
        )}
      </Formik>
    </Box>
  );
}

export default SignUp;
