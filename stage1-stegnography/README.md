# Stage 1: The Altered ID

## Challenge Description

An employee ID image may contain more information than is visible. Inspect the provided image carefully to discover the hidden message.

## Objective

Inspect the image and extract the hidden message to find the flag.

## Challenge File

* `challenge/rabbit_id.jpg`

## Suggested Tools

* ExifTool
* Steghide

## Instructions

1. Inspect the image and its metadata using ExifTool.
2. Use Steghide to check whether the image contains hidden data.
3. Extract the hidden message using the password provided through the challenge hints.
4. Find the flag in the extracted message.

## Learning Objectives

* Inspect image files and metadata.
* Understand image steganography.
* Identify and extract hidden data using Steghide.

## Flag Format

`FLAG{...}`
